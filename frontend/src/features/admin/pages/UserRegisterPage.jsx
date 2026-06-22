import React, { useState } from 'react'
import { useForm } from 'react-hook-form';
import { registerUser } from '../api/adminApi';
import { useNavigate } from 'react-router-dom';

function UserRegisterPage() {

    const [ serverError, setServerError] = useState(null);
    const navigate = useNavigate();

    const {
        register,
        handleSubmit,
        formState: { errors, isSubmitting }
    } = useForm();

    const onSubmit = async (data) => {
        try {
            setServerError(null);
            const response = await registerUser(data);
            console.log(`${data.username} registered with user id ${response.user_id}`);
            navigate("/");
        } catch(err) {
            console.error(err);
            serverError(
                err?.response?.data?.detail ||
                "Invalid credentials"
            )
        }
    }

  return (

    <div className="flex min-h-screen items-center justify-center bg-slate-50">
        <div className="w-full max-w-md rounded-lg border bg-white p-8 shadow-sm">

            <div className="mb-8 text-center">
                <h1 className="text-3xl font-bold">
                    Hospital ERP
                </h1>

                <p className="mt-2 text-gray-500">
                    Register new user
                </p>
            </div>

            <form onSubmit={handleSubmit(onSubmit)} className="space-y-4" >
                <div>
                    <label htmlFor="username" className="mb-1 block">Username </label>
                    <input {...register("username")}  className="w-full rounded-md border p-2"/>
                    {errors.username && errors.username.message}
                </div>
                <div>
                    <label htmlFor="email" className="mb-1 block" >Email </label>
                    <input {...register("email")} className="w-full rounded-md border p-2"/>
                    {errors.email && errors.email.message}
                </div>
                <div>
                    <label htmlFor="password">Password </label>
                    <input {...register("password")} className="w-full rounded-md border p-2"/>
                    {errors.password && errors.password.message}
                </div>
                <div>
                    <label htmlFor="role" className="mb-1 block" >Role </label>
                    <select {...register("role")} className="w-full border rounded-md p-2" >
                        <option value="" >Select Role</option>
                        <option value="DOCTOR" >Doctor</option>
                        <option value="RECEPTIONIST" >Receptionist</option>
                        <option value="ADMIN" >Admin</option>
                    </ select>
                    {errors.role && errors.role.message}
                </div>

                <button type='submit' disabled={isSubmitting}
                 className="w-full rounded-md bg-black px-4 py-2 text-white disabled:opacity-50">
                    {isSubmitting ? "Registering..." : "Register"}
                </button>

            </form>
        </div>
    </div>
  )
}

export default UserRegisterPage