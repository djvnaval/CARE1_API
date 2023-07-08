<?php

namespace App\Models\oneM2M_MQTT_AQM;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Jenssegers\Mongodb\Eloquent\Model;

class PM2_5_In extends Model
{
    use HasFactory;
    protected $connection = 'oneM2M_MQTT_AQM';
    protected $table = "PM2_5_in";
    protected $primaryKey = "_id";
}
