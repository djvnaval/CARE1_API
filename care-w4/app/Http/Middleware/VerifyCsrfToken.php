<?php

namespace App\Http\Middleware;

use Illuminate\Foundation\Http\Middleware\VerifyCsrfToken as Middleware;

class VerifyCsrfToken extends Middleware
{
    /**
     * The URIs that should be excluded from CSRF verification.
     *
     * @var array<int, string>
     */
    protected $except = [
        '/solenoid/actuation/change',
        '/filterFanSensor/actuation/change',
        '/windowSensor/actuation/change',
        '/solenoid/current',
        '/filterFanSensor/current',
        '/windowSensor/current',
        '/FilterFan/actuation/change',
        '/FilterFan/current',
        '/Window/current',
        '/Window/actuation/change',

    ];
}
