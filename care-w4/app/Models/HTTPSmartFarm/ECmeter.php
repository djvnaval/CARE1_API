<?php

namespace App\Models\HTTPSmartFarm;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Jenssegers\Mongodb\Eloquent\Model;

class ECmeter extends Model
{
    use HasFactory;
    protected $connection = 'HTTPSmartFarm';
    protected $table = "ECmeter";
    protected $primaryKey = "_id";
}
