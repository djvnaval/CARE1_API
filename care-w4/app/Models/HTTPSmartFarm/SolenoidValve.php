<?php

namespace App\Models\HTTPSmartFarm;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Jenssegers\Mongodb\Eloquent\Model;

class SolenoidValve extends Model
{
    use HasFactory;
    protected $connection = 'HTTPSmartFarm';
    protected $table = "solenoidValve";
    protected $primaryKey = "_id";
}
