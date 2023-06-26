<?php

namespace App\Models\HTTPSmartFarm;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Jenssegers\Mongodb\Eloquent\Model;

class WaterLevel extends Model
{
    use HasFactory;
    protected $connection = 'HTTPSmartFarm';
    protected $table = "waterLevel";
    protected $primaryKey = "_id";
}
