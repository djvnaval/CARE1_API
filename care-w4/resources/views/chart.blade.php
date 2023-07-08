@php
    use Carbon\Carbon;
@endphp
<x-guest-layout>
    @section('title', "$folder")
    @section('description', $folders[$folder][0])

    @section('breadcrumb')
        <x-breadcrumb-item href="/{{ $database }}/{{ $folder }}">{{ $database }}</x-breadcrumb-item>
        <x-breadcrumb-active>{{ $folder }}</x-breadcrumb-active>
    @endsection

    @section('controls')

    <form action="/{{ $database }}/{{ $folder }}/time-range" class="mb-5 float-right">
        <div class="hidden">
            <div class="days">
                <div class="days-of-week grid grid-cols-7 mb-1 dow block flex-1 leading-9 border-0 rounded-lg cursor-default text-center text-white font-semibold text-sm"></div>
                <div class="datepicker-grid w-64 grid grid-cols-7 block flex-1 leading-9 border-0 rounded-lg cursor-default text-center text-white font-semibold text-sm h-6 leading-6 text-sm font-medium text-gray-500 dark:text-gray-400"></div>
            </div>
            <div class="calendar-weeks">
                <div class="days-of-week flex"><span class="dow h-6 leading-6 text-sm font-medium text-gray-500 dark:text-gray-400"></span></div>
                <div class="weeks week block flex-1 leading-9 border-0 rounded-lg cursor-default text-center text-white font-semibold text-sm"></div>
            </div>
        </div>
        
        <div date-rangepicker class="flex items-center">
            <div class="relative">
              <div class="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">
                  <svg aria-hidden="true" class="w-5 h-5 text-gray-500 dark:text-gray-400" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M6 2a1 1 0 00-1 1v1H4a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V6a2 2 0 00-2-2h-1V3a1 1 0 10-2 0v1H7V3a1 1 0 00-1-1zm0 5a1 1 0 000 2h8a1 1 0 100-2H6z" clip-rule="evenodd"></path></svg>
              </div>
              <input id="hanz" class="text-black bg-gray-50 border border-gray-300 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-72 pl-10 p-2.5  dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" type="text" name="datetimes" value="{{ isset($start_date) && isset($end_date) ? Carbon::createFromFormat('m-d-Y H:i:s', $start_date)->format('m/d/Y H:i:s') . ' - ' . Carbon::createFromFormat('m-d-Y H:i:s', $end_date)->format('m/d/Y H:i:s') : '' }}"/>
            </div>

            <div class="relative">
                <button type="submit" class="ml-5 text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 mr-2 mb-2 dark:bg-blue-600 dark:hover:bg-blue-700 focus:outline-none dark:focus:ring-blue-800 mt-2">Go</button>
            </div>
        </div>
    </form>
    @endsection

    <div>
       <div class="mb-8">
            <x-toggle id="solenoid_status" 
                data-visible="{{ $solenoidValve_actuate ? $solenoidValve_actuate->value : 'null' }}" 
                class="toggle-buttons" 
                data-url="/solenoid/actuation/change" 
                data-update_url="/solenoid/current" 
                data-method="POST"
            >
                Solenoid Actuation
            </x-toggle>

            <x-toggle id="filterFanSensor_status" 
                data-visible="{{ $filterFanSensor_actuate ? $filterFanSensor_actuate->value : 'null' }}" 
                class="toggle-buttons" 
                data-url="/filterFanSensor/actuation/change" 
                data-update_url="/filterFanSensor/current" 
                data-method="POST"
            >
                Filter Fan Sensor
            </x-toggle>

            <x-toggle id="windowSensor_status" 
                data-visible="{{ $windowSensor_actuate ? $windowSensor_actuate->value : 'null' }}" 
                class="toggle-buttons" 
                data-url="/windowSensor/actuation/change"  
                data-update_url="/windowSensor/current"  
                data-method="POST"
            >
                Window Sensor
            </x-toggle>

            <x-toggle id="FilterFan_status" 
                data-visible="{{ $FilterFan_actuate ? $FilterFan_actuate->value : 'null' }}" 
                class="toggle-buttons" 
                data-url="/FilterFan/actuation/change" 
                data-update_url="/FilterFan/current" 
                data-method="POST"
            >
                Filter Fan Actuation
            </x-toggle>

            <x-toggle id="Window_status" 
                data-visible="{{ $Window_actuate ? $Window_actuate->value : 'null' }}" 
                class="toggle-buttons" 
                data-url="/Window/actuation/change" 
                data-update_url="/Window/current" 
                data-method="POST"
            >
                Window Actuation
            </x-toggle>
       </div>

        <div class="grid lg:grid-cols-5 md:grid-cols-4 md:gap-5 gap-x-0 gap-y-5 grid-cols-1">
            <div class="bg-[#37393f] rounded-3xl py-5 ">
                <canvas class="w-full max-h-[50vh] gauge-chart" data-value="{{ $min }}" data-label="Min"></canvas>
                <canvas class="w-full max-h-[50vh] gauge-chart mt-10" data-value="{{ $max }}" data-label="Max"></canvas>
                <canvas class="w-full max-h-[50vh] gauge-chart mt-10" data-value="{{ $average }}" data-label="Average"></canvas>  
            </div>
            <x-segment class="clear-right lg:col-span-4 md:cols-span-3 bg-[#37393f]">
                <canvas id="chart" class="w-full max-h-[50vh] "></canvas>
            </x-segment>
            <x-segment class="flex items-center lg:p-0 bg-[#37393f]">
                <canvas id="realtimeGauge" class="w-full max-h-[50vh] object-center" data-value="0" data-label="Realtime"></canvas>
            </x-segment>
            <x-segment class="clear-right lg:col-span-4 md:cols-span-3 bg-[#37393f]">
                <canvas id="realtimeChart" class="w-full max-h-[50vh] "></canvas>
            </x-segment>
        </div>
    </div>

    <script>
        const data = {!! $result ?? '""' !!};
        const database = "{{ $database }}";
        const folder = "{{ $folder }}";
        const solenoidValve_actuate = {!! $solenoidValve_actuate ?? "null" !!};
        const unit = "{{ $unit }}";
        const threshold = {{ json_encode($folders[$folder][1]) }};
        const csrf_token = "{{ csrf_token() }}";
    </script>
    
</x-guest-layout>
