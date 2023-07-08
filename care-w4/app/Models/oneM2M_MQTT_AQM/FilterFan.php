<?php

namespace App\Models\oneM2M_MQTT_AQM;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Jenssegers\Mongodb\Eloquent\Model;

class FilterFan extends Model
{
    use HasFactory;
    protected $connection = 'oneM2M_MQTT_AQM';
    protected $table = "FilterFan";
    protected $primaryKey = "_id";
}
