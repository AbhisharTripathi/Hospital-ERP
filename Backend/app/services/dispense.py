from fastapi import HTTPException, status

from app.models.dispense import (
    DispenseModel,
    DispensedMedicineModel,
    DispensedBatchModel
)

from app.models.prescription import PrescriptionStatus

from app.utils.id_generator import IDGenerator


class DispenseService:

    def __init__(
        self,
        dispense_repository,
        prescription_repository,
        batch_repository,
        stock_repository,
        stock_movement_repository,
        counter_repository
    ):

        self.dispense_repo = dispense_repository
        self.prescription_repo = prescription_repository
        self.batch_repo = batch_repository
        self.stock_repo = stock_repository
        self.stock_movement_repo = stock_movement_repository
        self.counter_repo = counter_repository


    # ==========================================
    # Dispense Prescription
    # ==========================================

    async def dispense_prescription(
        self,
        hospital_id: str,
        current_user,
        prescription_id: str
    ):

        user_id = current_user["user_id"]


        # ==========================================
        # 1. Get Prescription
        # ==========================================

        prescription = (
            await self.prescription_repo
            .get_by_prescription_id(
                hospital_id=hospital_id,
                prescription_id=prescription_id
            )
        )

        if not prescription:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Prescription not found"
            )


        # ==========================================
        # 2. Check Prescription Status
        # ==========================================

        if prescription["status"] != (
            PrescriptionStatus.ACTIVE.value
        ):

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only active prescription can be dispensed"
            )


        # ==========================================
        # 3. Check Already Dispensed
        # ==========================================

        existing_dispense = (
            await self.dispense_repo
            .get_by_prescription_id(
                hospital_id=hospital_id,
                prescription_id=prescription_id
            )
        )

        if existing_dispense:

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Prescription is already dispensed"
            )


        # ==========================================
        # 4. Create Stock Plan
        # ==========================================

        stock_plan = []


        for medicine in prescription["medicines"]:

            medicine_id = medicine["medicine_id"]
            medicine_name = medicine["medicine_name"]
            required_quantity = medicine["quantity"]

            remaining_quantity = required_quantity

            medicine_stock_plan = []


            # ==========================================
            # Get Batches
            # Batches are already sorted by expiry
            # ==========================================

            batches = (
                await self.batch_repo
                .get_by_medicine(
                    hospital_id=hospital_id,
                    medicine_id=medicine_id
                )
            )


            # ==========================================
            # Check Batches One By One
            # ==========================================

            for batch in batches:

                if remaining_quantity <= 0:
                    break


                batch_id = batch["batch_id"]


                # ==========================================
                # Get Stock For Batch
                # ==========================================

                stock = (
                    await self.stock_repo
                    .get_by_medicine_batch(
                        hospital_id=hospital_id,
                        medicine_id=medicine_id,
                        batch_id=batch_id
                    )
                )

                if not stock:
                    continue


                available_quantity = (
                    stock["available_quantity"]
                )

                if available_quantity <= 0:
                    continue


                # ==========================================
                # Decide How Much To Take
                # ==========================================

                consume_quantity = min(
                    remaining_quantity,
                    available_quantity
                )


                # ==========================================
                # Add To Stock Plan
                # ==========================================

                medicine_stock_plan.append({

                    "medicine_id": medicine_id,

                    "medicine_name": medicine_name,

                    "batch_id": batch_id,

                    "batch_number": batch["batch_number"],

                    "stock_id": stock["stock_id"],

                    "quantity": consume_quantity
                })


                remaining_quantity -= consume_quantity


            # ==========================================
            # Check Sufficient Stock
            # ==========================================

            if remaining_quantity > 0:

                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=(
                        f"Insufficient stock for medicine: "
                        f"{medicine_name}. "
                        f"Remaining quantity: "
                        f"{remaining_quantity}"
                    )
                )


            # ==========================================
            # Add Medicine Plan To Main Stock Plan
            # ==========================================

            stock_plan.extend(
                medicine_stock_plan
            )


        # ==========================================
        # IMPORTANT:
        # Up to this point NO stock is deducted.
        #
        # If any medicine has insufficient stock,
        # the function has already stopped above.
        # ==========================================


        # ==========================================
        # 5. Execute Stock Plan
        # ==========================================

        dispensed_medicines = []


        for medicine in prescription["medicines"]:

            medicine_id = medicine["medicine_id"]
            medicine_name = medicine["medicine_name"]
            required_quantity = medicine["quantity"]

            dispensed_batches = []


            # ==========================================
            # Get Plan For Current Medicine
            # ==========================================

            medicine_plan = [

                item
                for item in stock_plan

                if item["medicine_id"] == medicine_id
            ]


            # ==========================================
            # Process Each Batch
            # ==========================================

            for item in medicine_plan:


                # ==========================================
                # Decrease Stock
                # ==========================================

                result = (
                    await self.stock_repo
                    .decrease_quantity(
                        hospital_id=hospital_id,
                        stock_id=item["stock_id"],
                        quantity=item["quantity"]
                    )
                )


                if result.modified_count == 0:

                    raise HTTPException(
                        status_code=status.HTTP_409_CONFLICT,
                        detail=(
                            "Stock changed while dispensing. "
                            "Please try again."
                        )
                    )


                # ==========================================
                # Generate Stock Movement ID
                # ==========================================

                movement_id = (
                    await IDGenerator
                    .generate_stock_movement_id(
                        self.counter_repo
                    )
                )


                # ==========================================
                # Create OUT Movement
                # ==========================================

                movement_data = {

                    "movement_id": movement_id,

                    "hospital_id": hospital_id,

                    "stock_id": item["stock_id"],

                    "medicine_id": medicine_id,

                    "batch_id": item["batch_id"],

                    "movement_type": "OUT",

                    "quantity": item["quantity"],

                    "reference_type": "PRESCRIPTION",

                    "reference_id": prescription_id,

                    "reason": "Medicine dispensed",

                    "created_by": user_id
                }


                await self.stock_movement_repo.create_movement(
                    movement_data
                )


                # ==========================================
                # Add Batch To Dispense Response
                # ==========================================

                dispensed_batches.append(

                    DispensedBatchModel(

                        medicine_id=medicine_id,

                        batch_id=item["batch_id"],

                        batch_number=item["batch_number"],

                        quantity=item["quantity"]
                    )
                )


            # ==========================================
            # Build Dispensed Medicine
            # ==========================================

            dispensed_medicines.append(

                DispensedMedicineModel(

                    medicine_id=medicine_id,

                    medicine_name=medicine_name,

                    prescribed_quantity=required_quantity,

                    dispensed_quantity=required_quantity,

                    batches=dispensed_batches
                )
            )


        # ==========================================
        # 6. Generate Dispense ID
        # ==========================================

        dispense_id = (
            await IDGenerator
            .generate_dispense_id(
                self.counter_repo
            )
        )


        # ==========================================
        # 7. Create Dispense Record
        # ==========================================

        dispense = DispenseModel(

            dispense_id=dispense_id,

            hospital_id=hospital_id,

            prescription_id=prescription_id,

            patient_id=prescription["patient_id"],

            dispensed_by=user_id,

            medicines=dispensed_medicines
        )


        await self.dispense_repo.create_dispense(

            dispense.model_dump()
        )


        # ==========================================
        # 8. Return Dispense
        # ==========================================

        return dispense