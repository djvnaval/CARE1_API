<?php

namespace App\Models\oneM2M_MQTT_SmartFarm;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Jenssegers\Mongodb\Eloquent\Model;

class ElecConductivity extends Model
{
    use HasFactory;
    protected $connection = 'oneM2M_MQTT_SmartFarm';
    protected $table = "ElecConductivity";
    protected $primaryKey = "_id";
}
