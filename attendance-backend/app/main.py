# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware

# from app.routers import auth_routes, admin_routes, attendance_routes, leave_routes, salary_routes, face_attendance_routes, rag_routes,admin_agent_routes, cost_tracker_routes

# from app.scheduler import start_scheduler

# app = FastAPI(title="Face Attendance System API")

# app.include_router(auth_routes.router)
# app.include_router(admin_routes.router)
# app.include_router(attendance_routes.router)
# app.include_router(leave_routes.router)
# app.include_router(salary_routes.router)
# app.include_router(face_attendance_routes.router)
# app.include_router(rag_routes.router)
# app.include_router(admin_agent_routes.router)  # Add the admin agent routes
# app.include_router(cost_tracker_routes.router)  # Add the cost tracker routes
# # Allow the React frontend (running on a different port) to call this API
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:5173", "http://localhost:3000"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# app.include_router(auth_routes.router)

# @app.on_event("startup")
# def on_startup():
#     start_scheduler()


# @app.get("/")
# def root():
#     return {"message": "Face Attendance System API is running"}


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import auth_routes, admin_routes, attendance_routes, leave_routes, salary_routes, face_attendance_routes, rag_routes, admin_agent_routes, cost_tracker_routes
from app.scheduler import start_scheduler

app = FastAPI(title="Face Attendance System API")

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:5173", "http://localhost:3000"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_routes.router)
app.include_router(admin_routes.router)
app.include_router(attendance_routes.router)
app.include_router(leave_routes.router)
app.include_router(salary_routes.router)
app.include_router(face_attendance_routes.router)
app.include_router(rag_routes.router)
app.include_router(admin_agent_routes.router)
app.include_router(cost_tracker_routes.router)


@app.on_event("startup")
def on_startup():
    start_scheduler()


@app.get("/")
def root():
    return {"message": "Face Attendance System API is running"}