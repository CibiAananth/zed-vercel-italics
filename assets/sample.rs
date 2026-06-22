use std::fmt;

#[derive(Clone, Debug, PartialEq, Eq)]
pub enum UserRole {
    Admin,
    Member,
    Guest,
}

impl fmt::Display for UserRole {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        let label = match self {
            Self::Admin => "admin",
            Self::Member => "member",
            Self::Guest => "guest",
        };
        write!(f, "{label}")
    }
}

#[derive(Clone, Debug)]
pub struct User {
    pub id: String,
    pub name: String,
    pub role: UserRole,
    pub active: bool,
}

pub trait UserRepository {
    fn find_by_id(&self, id: &str) -> Option<User>;
    fn save(&mut self, user: User) -> Result<(), String>;
}

/// Returns a stable cache key for the user record.
pub fn cache_key(user: &User) -> String {
    format!("{}:{}:{}", user.id, user.role, user.active)
}

pub fn load_user(repo: &dyn UserRepository, id: &str) -> Option<User> {
    // Skip lookup for empty ids.
    if id.trim().is_empty() {
        return None;
    }

    let user = repo.find_by_id(id)?;
    if user.active {
        println!("Loaded {} ({})", user.name, user.role);
    }

    Some(user)
}
