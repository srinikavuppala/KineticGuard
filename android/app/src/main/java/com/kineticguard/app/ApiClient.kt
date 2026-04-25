package com.kineticguard.app

import com.google.gson.annotations.SerializedName
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import retrofit2.http.Body
import retrofit2.http.Header
import retrofit2.http.POST

data class SosRequest(
    @SerializedName("trigger_method") val triggerMethod: String = "GESTURE",
    @SerializedName("latitude") val latitude: Double,
    @SerializedName("longitude") val longitude: Double
)

data class SosResponse(
    @SerializedName("id") val id: String,
    @SerializedName("status") val status: String
)

// NEW: Login data classes
data class LoginRequest(
    @SerializedName("email") val email: String,
    @SerializedName("password") val password: String
)

data class LoginResponse(
    @SerializedName("access_token") val accessToken: String,
    @SerializedName("token_type") val tokenType: String = "bearer"
)

interface ApiInterface {
    @POST("api/v1/auth/login")
    suspend fun login(@Body request: LoginRequest): LoginResponse

    @POST("api/v1/alerts/trigger")
    suspend fun sendSos(
        @Header("Authorization") token: String,
        @Body request: SosRequest
    ): SosResponse
}

object ApiClient {
    private const val BASE_URL = "http://192.168.0.2:8000/" // Updated to match your backend logs

    val instance: ApiInterface by lazy {
        Retrofit.Builder()
            .baseUrl(BASE_URL)
            .addConverterFactory(GsonConverterFactory.create())
            .build()
            .create(ApiInterface::class.java)
    }
}