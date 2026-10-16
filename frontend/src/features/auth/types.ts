export type UserRole = "SUPER_ADMIN" | "SHOP_ADMIN" | "AGENT" | "CUSTOMER";
export interface AuthUser { id: number | string; username: string; full_name: string; role: UserRole; shop_id: number | string | null; shop_name: string | null; must_change_password: boolean }
export interface LoginPayload { username: string; password: string }
export interface LoginResponse { access: string; refresh: string; user: AuthUser }
export interface RefreshResponse { access: string }
export interface ChangePasswordPayload { old_password: string; new_password: string }
