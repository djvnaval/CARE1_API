<?php

namespace App\Models\HTTPSmartFarm;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Jenssegers\Mongodb\Eloquent\Model;

class PHsensor extends Model
{
    use HasFactory;
    protected $connection = 'HTTPSmartFarm';
    protected $table = "pHsensor";
    protected $primaryKey = "_id";
}
