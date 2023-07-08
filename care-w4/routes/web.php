<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\Chart;
use App\Http\Controllers\HTTPSmartFarm\SolenoidValve_actuateController;
use App\Http\Controllers\HTTPAQM\WindowSensor_actuateController;
use App\Http\Controllers\HTTPAQM\FilterFanSensor_actuateController;
use App\Http\Controllers\HTTPSmartFarm\SolenoidValveController;
use App\Http\Controllers\HTTPAQM\WindowSensorController;
use App\Http\Controllers\HTTPAQM\FilterFanSensorController;
use App\Http\Controllers\oneM2M_MQTT_AQM\Window_actuateController;
use App\Http\Controllers\oneM2M_MQTT_AQM\FilterFan_actuateController;
use App\Http\Controllers\oneM2M_MQTT_AQM\WindowController;
use App\Http\Controllers\oneM2M_MQTT_AQM\FilterFanController;

use App\Models\Node;

/*
|--------------------------------------------------------------------------
| Web Routes
|--------------------------------------------------------------------------
|
| Here is where you can register web routes for your application. These
| routes are loaded by the RouteServiceProvider within a group which
| contains the "web" middleware group. Now create something great!
|
*/

Route::get('/sample', fn() => view('sample'));
Route::get('/', [Chart::class, 'home']);

Route::get('/nodes', function() {
    $node = new Node;
    $node->value = 1;
    $node->save();
});

Route::get('/{database}/{folder}/time-range', [Chart::class, 'timeRange']);
Route::get('/realtime/{database}/{folder}/{start_date?}/{end_date?}',[Chart::class, 'realtimeChart']);

Route::get('/{database}/{folder}/{start_date?}/{end_date?}',[Chart::class, 'chart']);

Route::post('/solenoid/actuation/change', [SolenoidValve_actuateController::class, 'store']);
Route::post('/filterFanSensor/actuation/change', [FilterFanSensor_actuateController::class, 'store']);
Route::post('/windowSensor/actuation/change', [WindowSensor_actuateController::class, 'store']);
Route::post('/FilterFan/actuation/change', [FilterFan_actuateController::class, 'store']);
Route::post('/Window/actuation/change', [Window_actuateController::class, 'store']);

Route::post('/solenoid/current', [SolenoidValveController::class, 'show']);
Route::post('/filterFanSensor/current', [FilterFanSensorController::class, 'show']);
Route::post('/windowSensor/current', [WindowSensorController::class, 'show']);
Route::post('/FilterFan/current', [FilterFanController::class, 'show']);
Route::post('/Window/current', [WindowController::class, 'show']);

Route::middleware([ 
    'auth:sanctum',
    config('jetstream.auth_session'),
    'verified'
])->group(function () {
    Route::get('/dashboard', function () {
        return view('dashboard');
    })->name('dashboard');
});
