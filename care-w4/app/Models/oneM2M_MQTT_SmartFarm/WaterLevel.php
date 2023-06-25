<?php

namespace App\Models\oneM2M_MQTT_SmartFarm;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Jenssegers\Mongodb\Eloquent\Model;

class WaterLevel extends Model
{
    use HasFactory;
    protected $connection = 'oneM2M_MQTT_SmartFarm';
    protected $table = "WaterLevel";
    protected $primaryKey = "_id";
}
