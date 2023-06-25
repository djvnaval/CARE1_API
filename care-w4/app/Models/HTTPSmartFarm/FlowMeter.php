<?php

namespace App\Models\HTTPSmartFarm;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Jenssegers\Mongodb\Eloquent\Model;

class FlowMeter extends Model
{
    use HasFactory;
    protected $connection = 'HTTPSmartFarm';
    protected $table = "flowMeter";
    protected $primaryKey = "_id";
}
