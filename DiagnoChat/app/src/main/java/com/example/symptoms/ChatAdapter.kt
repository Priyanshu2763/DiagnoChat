package com.example.symptoms

import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import androidx.recyclerview.widget.RecyclerView

class ChatAdapter(private val messages: List<ChatMessage>) :
    RecyclerView.Adapter<ChatAdapter.ChatViewHolder>() {

    inner class ChatViewHolder(itemView: View) : RecyclerView.ViewHolder(itemView) {
        val messageText: TextView = itemView.findViewById(R.id.messageText)
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ChatViewHolder {
        val view = LayoutInflater.from(parent.context)
            .inflate(R.layout.chat_item, parent, false)
        return ChatViewHolder(view)
    }

    override fun onBindViewHolder(holder: ChatViewHolder, position: Int) {
        val message = messages[position]
        holder.messageText.text = message.message

        val layoutParams = holder.messageText.layoutParams as ViewGroup.MarginLayoutParams
        if (message.isUser) {
            holder.messageText.setBackgroundResource(R.drawable.chat_bubble_user)
            layoutParams.marginStart = 50
            layoutParams.marginEnd = 0
        } else {
            holder.messageText.setBackgroundResource(R.drawable.chat_bubble_bot)
            layoutParams.marginStart = 0
            layoutParams.marginEnd = 50
        }
        holder.messageText.layoutParams = layoutParams
    }

    override fun getItemCount(): Int = messages.size
}
