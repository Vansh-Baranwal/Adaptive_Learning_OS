/* ------------------------------------------------------------------ */
/*  TypeScript interfaces matching exact backend Pydantic schemas      */
/* ------------------------------------------------------------------ */

// ────────── Auth ──────────
export interface UserCreate {
  email: string;
  password: string;
  first_name: string;
  last_name: string;
  role: "student" | "teacher";
  department?: string;
}

export interface UserResponse {
  id: number;
  email: string;
  role: "student" | "teacher";
  is_active: boolean;
  created_at: string;
}

export interface Token {
  access_token: string;
  token_type: string;
}

// ────────── Student / Teacher ──────────
export interface StudentResponse {
  id: number;
  user_id: number;
  first_name: string;
  last_name: string;
  enrolled_at: string;
}

export interface TeacherResponse {
  id: number;
  user_id: number;
  first_name: string;
  last_name: string;
  department: string | null;
}

// ────────── Concept ──────────
export interface ConceptCreate {
  name: string;
  description?: string;
  difficulty_level?: number;
  prerequisite_id?: number | null;
}

export interface ConceptResponse {
  id: number;
  name: string;
  description: string | null;
  difficulty_level: number;
  prerequisite_id: number | null;
  created_at: string;
}

// ────────── Assignment ──────────
export interface AssignmentCreate {
  title: string;
  description?: string;
  rubric?: Record<string, unknown>;
  due_date?: string | null;
  concept_id: number;
  teacher_id: number;
}

export interface AssignmentResponse {
  id: number;
  title: string;
  description: string | null;
  rubric: Record<string, unknown> | null;
  due_date: string | null;
  concept_id: number;
  teacher_id: number;
  created_at: string;
}

// ────────── Attempt ──────────
export interface AttemptCreate {
  content: string;
  student_id: number;
  assignment_id: number;
  concept_id: number;
}

export interface AttemptResponse {
  id: number;
  content: string;
  student_id: number;
  assignment_id: number;
  concept_id: number;
  score: number | null;
  evaluation: Record<string, unknown> | null;
  submitted_at: string;
}

// ────────── Mastery ──────────
export interface MasteryResponse {
  id: number;
  student_id: number;
  concept_id: number;
  p_l: number; // Current mastery probability
  p_t: number; // Learning rate
  p_g: number; // Guess probability
  p_s: number; // Slip probability
  attempt_count: number;
  last_updated: string;
}

// ────────── Prediction ──────────
export interface MasteryPrediction {
  student_id: number;
  concept_id: number;
  predicted_mastery: number;
}
