package com.example.symptoms
// ApiService.kt
import retrofit2.Call
import retrofit2.http.Body
import retrofit2.http.Headers
import retrofit2.http.POST

data class SymptomRequest(val symptoms: List<String>)
data class PredictionResponse(
    val predicted_disease: String,
    val top_5_predictions: List<TopPrediction>
)

data class TopPrediction(val disease: String, val probability: Double)

interface ApiService {
    @Headers("Content-Type: application/json")
    @POST("/predict")
    fun getPrediction(@Body request: SymptomRequest): Call<PredictionResponse>
}
