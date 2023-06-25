<?php

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;

use App\Models\HTTPSmartFarm\Dht22Humi;
use App\Models\HTTPSmartFarm\Dht22Temp;
use App\Models\HTTPSmartFarm\ECmeter;
use App\Models\HTTPSmartFarm\FlowMeter;
use App\Models\HTTPSmartFarm\MotorSensor;
use App\Models\HTTPSmartFarm\OverflowSensor;
use App\Models\HTTPSmartFarm\PHsensor;
use App\Models\HTTPSmartFarm\SolenoidValve;
use App\Models\HTTPSmartFarm\WaterLevel as WaterLevel_HTTP_FARM;

use App\Models\HTTPSmartFarm_actuate\SolenoidValve_actuate;

use App\Models\oneM2M_HTTP_AQM\PM2_5 as PM2_5_HTTP;

use App\Models\oneM2M_MQTT_AQM\PM2_5 as PM2_5_MQTT;
use App\Models\oneM2M_MQTT_AQM\H2S;
use App\Models\oneM2M_MQTT_AQM\Humidity as Humidity_MQTT_AQM;
use App\Models\oneM2M_MQTT_AQM\PM10;
use App\Models\oneM2M_MQTT_AQM\Temperature as Temperature_MQTT_AQM;

use App\Models\oneM2M_MQTT_SmartFarm\ElecConductivity;
use App\Models\oneM2M_MQTT_SmartFarm\Env_Temp;
use App\Models\oneM2M_MQTT_SmartFarm\Humidity as Humidity_MQTT_FARM;
use App\Models\oneM2M_MQTT_SmartFarm\PH;
use App\Models\oneM2M_MQTT_SmartFarm\Sol_Temp;
use App\Models\oneM2M_MQTT_SmartFarm\Temperature as Temperature_MQTT_FARM;
use App\Models\oneM2M_MQTT_SmartFarm\WaterLevel as WaterLevel_MQTT_FARM;

use App\Models\HTTPAQM\PM2_5_Indoor;
use App\Models\HTTPAQM\PM2_5_Outdoor;
use App\Models\HTTPAQM\Dht22Humi as Dht22Humi_HTTP_AQM;
use App\Models\HTTPAQM\Dht22Temp as Dht22Temp_HTTP_AQM;
use App\Models\HTTPAQM\FilterFanSensor;
use App\Models\HTTPAQM\WindowSensor;

use App\Models\HTTPAQM_actuate\FilterFanSensor_actuate;
use App\Models\HTTPAQM_actuate\WindowSensor_actuate;

/*
|--------------------------------------------------------------------------
| API Routes
|--------------------------------------------------------------------------
|
| Here is where you can register API routes for your application. These
| routes are loaded by the RouteServiceProvider within a group which
| is assigned the "api" middleware group. Enjoy building your API!
|
*/

Route::middleware('auth:sanctum')->get('/user', function (Request $request) {
    return $request->user();
});

Route::middleware('auth:sanctum')->group(function(){
    Route::get('/HTTPSmartFarm/', []);
});
