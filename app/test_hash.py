from app.security import hash_password, verify_password

password = "abc123"

hashed = hash_password(password)

print("Original:", password)
print("Hashed:", hashed)

print(
    verify_password(
        "abc123",
        hashed
    )
)

print(
    verify_password(
        "wrongpassword",
        hashed
    )
)