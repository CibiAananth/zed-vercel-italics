package main

import (
	"context"
	"crypto/sha256"
	"encoding/hex"
	"fmt"
	"strings"
)

type UserRole string

const (
	RoleAdmin  UserRole = "admin"
	RoleMember UserRole = "member"
	RoleGuest  UserRole = "guest"
)

type User struct {
	ID     string
	Name   string
	Role   UserRole
	Active bool
}

type UserRepository interface {
	FindByID(ctx context.Context, id string) (*User, error)
	Save(ctx context.Context, user User) error
}

// HashUser returns a stable hash for cache keys.
func HashUser(user User) string {
	payload := fmt.Sprintf("%s:%s:%t", user.ID, user.Role, user.Active)
	sum := sha256.Sum256([]byte(payload))
	return hex.EncodeToString(sum[:])
}

func LoadUser(ctx context.Context, repo UserRepository, id string) (*User, error) {
	// Skip lookup for empty ids.
	if strings.TrimSpace(id) == "" {
		return nil, nil
	}

	user, err := repo.FindByID(ctx, id)
	if err != nil {
		return nil, fmt.Errorf("find user: %w", err)
	}

	if user != nil && user.Active {
		fmt.Printf("Loaded %s (%s)\n", user.Name, user.Role)
	}

	return user, nil
}
