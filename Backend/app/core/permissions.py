from fastapi import HTTPException, status

from app.models.user import UserRole


ROLE_HIERARCHY = {

    UserRole.SUPER_ADMIN: [

        UserRole.ADMIN,
        UserRole.DOCTOR,
        UserRole.NURSE,
        UserRole.RECEPTIONIST,
        UserRole.PHARMACIST,
        UserRole.LAB_TECHNICIAN,
        UserRole.ACCOUNTANT,
        UserRole.PATIENT,
    ],

    UserRole.ADMIN: [

        UserRole.DOCTOR,
        UserRole.NURSE,
        UserRole.RECEPTIONIST,
        UserRole.PHARMACIST,
        UserRole.LAB_TECHNICIAN,
        UserRole.ACCOUNTANT,
        UserRole.PATIENT,
    ]
}


def can_assign_role(
    current_role: UserRole,
    target_role: UserRole
):

    allowed_roles = ROLE_HIERARCHY.get(
        current_role,
        []
    )

    if target_role not in allowed_roles:

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"{current_role} cannot assign {target_role}"
        )


def can_manage_user(
    current_role: UserRole,
    target_role: UserRole
):

    allowed_roles = ROLE_HIERARCHY.get(
        current_role,
        []
    )

    if target_role not in allowed_roles:

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"{current_role} cannot manage {target_role}"
        )