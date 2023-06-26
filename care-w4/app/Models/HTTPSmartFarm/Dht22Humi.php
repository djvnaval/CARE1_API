<?php

namespace App\Models\HTTPSmartFarm;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Jenssegers\Mongodb\Eloquent\Model;

class Dht22Humi extends Model
{
    use HasFactory;
    protected $connection = 'HTTPSmartFarm';
    protected $table = "dht22Humi";
    protected $primaryKey = "_id";
}
