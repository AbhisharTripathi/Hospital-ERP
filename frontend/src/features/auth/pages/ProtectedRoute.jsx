import React from 'react'
import { Outlet } from 'react-router-dom'

function ProtectedRoute( {children}) {
  return (
    <div>{children}</div>
  )
}

export default ProtectedRoute