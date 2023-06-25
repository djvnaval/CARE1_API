<?php

namespace App\Models\oneM2M_HTTP_AQM;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Jenssegers\Mongodb\Eloquent\Model;

class PM2_5 extends Model
{
    use HasFactory;
    protected $connection = 'oneM2M_HTTP_AQM';
    protected $table = "PM2_5";
    protected $primaryKey = "_id";
}
