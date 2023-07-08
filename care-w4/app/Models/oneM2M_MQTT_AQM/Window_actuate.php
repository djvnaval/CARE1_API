<?php

namespace App\Models\oneM2M_MQTT_AQM;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Jenssegers\Mongodb\Eloquent\Model;

class Window_actuate extends Model
{
    use HasFactory;
    protected $connection = 'oneM2M_MQTT_AQM';
    protected $table = "Window_actuate";
    protected $primaryKey = "_id";

    protected $fillable = [
        'value', 
        'type', 
        'unit', 
        'time',
    ];
}
