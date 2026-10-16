export interface ApiError { status: number; code: string; detail: string; fields?: Record<string, string[]> }
export interface Paginated<T> { count: number; next: string | null; previous: string | null; results: T[] }
export interface ApiErrorBody { code?: string; detail?: string; fields?: Record<string, string[]> }
