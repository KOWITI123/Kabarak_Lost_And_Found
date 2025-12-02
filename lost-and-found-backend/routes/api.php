<?php

use App\Http\Controllers\AdminController;
use App\Http\Controllers\AuthController;
use App\Http\Controllers\ItemController;
use App\Http\Controllers\WhatsAppController;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;

/*
|--------------------------------------------------------------------------
| API Routes
|--------------------------------------------------------------------------
|
| Here is where you can register API routes for your application. These
| routes are loaded by the RouteServiceProvider and all of them will
| be assigned to the "api" middleware group. Make something great!
|
*/

// Public Routes
Route::post('/login', [AuthController::class, 'login']);

Route::get('/items', [ItemController::class, 'index']);
Route::post('/items/report', [ItemController::class, 'store']);
Route::post('/claims', [ItemController::class, 'storeClaim']);

Route::post('/webhook/whatsapp', [WhatsAppController::class, 'handleWebhook']);

// Protected Routes (Admin)
Route::middleware('auth:sanctum')->group(function () {
    Route::post('/logout', [AuthController::class, 'logout']);

    Route::prefix('admin')->group(function () {
        Route::get('/claims', [AdminController::class, 'getClaims']);
        Route::put('/claims/{id}', [AdminController::class, 'updateClaim']);
        Route::get('/stats', [AdminController::class, 'getStats']);
    });
    
    Route::get('/user', function (Request $request) {
        return $request->user();
    });
});
