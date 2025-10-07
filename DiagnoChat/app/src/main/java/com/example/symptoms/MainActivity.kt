package com.example.symptoms

import android.os.Bundle
import android.widget.EditText
import android.widget.ImageButton
import androidx.appcompat.app.AppCompatActivity
import androidx.appcompat.widget.Toolbar
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import retrofit2.http.Body
import retrofit2.http.Headers
import retrofit2.http.POST
import com.google.gson.annotations.SerializedName

class MainActivity : AppCompatActivity() {

    private lateinit var chatRecyclerView: RecyclerView
    private lateinit var inputMessage: EditText
    private lateinit var sendButton: ImageButton
    private val messageList = mutableListOf<ChatMessage>()
    private lateinit var chatAdapter: ChatAdapter

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        val toolbar: Toolbar = findViewById(R.id.toolbar)
        setSupportActionBar(toolbar)
        supportActionBar?.title = "DiagnoChat"

        chatRecyclerView = findViewById(R.id.chatRecyclerView)
        inputMessage = findViewById(R.id.inputMessage)
        sendButton = findViewById(R.id.sendButton)

        chatAdapter = ChatAdapter(messageList)
        chatRecyclerView.layoutManager = LinearLayoutManager(this)
        chatRecyclerView.adapter = chatAdapter

        sendButton.setOnClickListener {
            val userMessage = inputMessage.text.toString().trim()
            if (userMessage.isNotEmpty()) {
                addMessage(userMessage, isUser = true)
                inputMessage.text.clear()

                val symptomsList = userMessage.split(",", " ")
                    .map { it.trim().lowercase() }
                    .filter { it.isNotEmpty() }

                addMessage("Processing your symptoms...", isUser = false)

                val request = SymptomRequest(symptomsList)
                RetrofitClient.instance.getPrediction(request).enqueue(object : Callback<PredictionResponse> {
                    override fun onResponse(call: Call<PredictionResponse>, response: Response<PredictionResponse>) {
                        if (response.isSuccessful) {
                            val prediction = response.body()?.predicted_disease ?: "Unknown"
                            addMessage("Predicted disease: $prediction", isUser = false)
                        } else {
                            addMessage("Server error: ${response.code()}", isUser = false)
                        }
                    }

                    override fun onFailure(call: Call<PredictionResponse>, t: Throwable) {
                        addMessage("Failed to connect: ${t.message}", isUser = false)
                    }
                })
            }
        }
    }

    private fun addMessage(message: String, isUser: Boolean) {
        messageList.add(ChatMessage(message, isUser))
        chatAdapter.notifyItemInserted(messageList.size - 1)
        chatRecyclerView.scrollToPosition(messageList.size - 1)
    }
}

// Retrofit data classes and interface

