function generatePassword() {
  // Set the password length
  const length = 16;

  // Set the possible password characters
  const chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+-=[]{}|;:,.<>/?';

  let password = '';

  for (let i = 0; i < length; i++) {
    // Get a random character from the possible characters
    const randomChar = chars[Math.floor(Math.random() * chars.length)];

    // Append the character to the password string
    password += randomChar;
  }

  return password;
}

// Generate a new password
const newPassword = generatePassword();

console.log(newPassword);
