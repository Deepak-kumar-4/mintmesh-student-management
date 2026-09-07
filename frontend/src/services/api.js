import axios from "axios";

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || "http://localhost:8000",
});

export function getStudents({ page, pageSize, enrollmentStatus } = {}) {
  const params = { page, page_size: pageSize };
  if (enrollmentStatus) {
    params.enrollment_status = enrollmentStatus;
  }
  return apiClient.get("/students", { params });
}

export function getStudent(id) {
  return apiClient.get(`/students/${id}`);
}

export function createStudent(data) {
  return apiClient.post("/students", data);
}

export function updateStudent(id, data) {
  return apiClient.patch(`/students/${id}`, data);
}

export function deleteStudent(id) {
  return apiClient.delete(`/students/${id}`);
}
