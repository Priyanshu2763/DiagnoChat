package com.example.symptoms
import android.os.Bundle
import android.widget.Button
import android.widget.EditText
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity

class RegisterActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_register) // Replace with your actual XML filename if different

        val emailInput = findViewById<EditText>(R.id.emailInput)
        val usernameInput = findViewById<EditText>(R.id.usernameInput1)
        val passwordInput = findViewById<EditText>(R.id.passwordInput1)
        val signUpButton = findViewById<Button>(R.id.signup_btn)

        signUpButton.setOnClickListener {
            val email = emailInput.text.toString().trim()
            val username = usernameInput.text.toString().trim()
            val password = passwordInput.text.toString().trim()

            if (email.isEmpty() || username.isEmpty() || password.isEmpty()) {
                Toast.makeText(this, "Please fill in all fields", Toast.LENGTH_SHORT).show()
            } else {
                // For now, just show a success toast
                Toast.makeText(this, "Registered Successfully!", Toast.LENGTH_SHORT).show()

                // TODO: Save user or proceed to LoginActivity or MainActivity
            }
        }
    }
}
