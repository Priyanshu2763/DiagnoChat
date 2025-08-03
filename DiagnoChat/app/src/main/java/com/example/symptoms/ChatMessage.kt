package com.example.symptoms

data class ChatMessage(
    val message: String,
    val isUser: Boolean // true = user, false = bot
)
