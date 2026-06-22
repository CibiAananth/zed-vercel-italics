import { createHash } from "node:crypto";

type UserId = string;
type UserRole = "admin" | "member" | "guest";

interface User {
  id: UserId;
  name: string;
  role: UserRole;
  active: boolean;
}

type UserRepository = {
  findById(id: UserId): Promise<User | null>;
  save(user: User): Promise<void>;
};

/** Returns a stable hash for cache keys. */
function hashUser(user: User): string {
  const payload = `${user.id}:${user.role}:${user.active}`;
  return createHash("sha256").update(payload).digest("hex");
}

async function loadUser(
  repo: UserRepository,
  id: UserId,
): Promise<User | null> {
  // Skip lookup for empty ids.
  if (!id.trim()) {
    return null;
  }

  const user = await repo.findById(id);
  if (user?.active) {
    console.info(`Loaded ${user.name} (${user.role})`);
  }

  return user ?? null;
}

export { hashUser, loadUser, type User, type UserRepository };
