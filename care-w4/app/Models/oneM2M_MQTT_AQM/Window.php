<?php

namespace App\Models\oneM2M_MQTT_AQM;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Jenssegers\Mongodb\Eloquent\Model;

class Window extends Model
{
    use HasFactory;
    protected $connection = 'oneM2M_MQTT_AQM';
    protected $table = "Window";
    protected $primaryKey = "_id";
}
