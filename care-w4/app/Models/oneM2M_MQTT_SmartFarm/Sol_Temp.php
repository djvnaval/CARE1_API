<?php

namespace App\Models\oneM2M_MQTT_SmartFarm;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Jenssegers\Mongodb\Eloquent\Model;

class Sol_Temp extends Model
{
    use HasFactory;
    protected $connection = 'oneM2M_MQTT_AQM';
    protected $table = "Sol_Temp";
    protected $primaryKey = "_id";
}
