<?php

namespace App\Models\oneM2M_MQTT_SmartFarm;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Jenssegers\Mongodb\Eloquent\Model;

class Env_Temp extends Model
{
    use HasFactory;
    protected $connection = 'oneM2M_MQTT_AQM';
    protected $table = "Env_Temp";
    protected $primaryKey = "_id";
}
