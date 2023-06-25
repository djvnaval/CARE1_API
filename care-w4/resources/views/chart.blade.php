<x-guest-layout>
    @section('title', "$folder")

    @section('breadcrumb')
        <x-breadcrumb-item href="/{{ $database }}/{{ $folders[0] }}">{{ $database }}</x-breadcrumb-item>
        <x-breadcrumb-active>{{ $folder }}</x-breadcrumb-active>
    @endsection

    @section('controls')

    <form action="/{{ $database }}/{{ $folder }}/time-range" class="mb-5 float-right">
        <div class="hidden">
            <div class="days">
                <div class="days-of-week grid grid-cols-7 mb-1 dow block flex-1 leading-9 border-0 rounded-lg cursor-default text-center text-gray-900 font-semibold text-sm"></div>
                <div class="datepicker-grid w-64 grid grid-cols-7 block flex-1 leading-9 border-0 rounded-lg cursor-default text-center text-gray-900 font-semibold text-sm h-6 leading-6 text-sm font-medium text-gray-500 dark:text-gray-400"></div>
            </div>
            <div class="calendar-weeks">
                <div class="days-of-week flex"><span class="dow h-6 leading-6 text-sm font-medium text-gray-500 dark:text-gray-400"></span></div>
                <div class="weeks week block flex-1 leading-9 border-0 rounded-lg cursor-default text-center text-gray-900 font-semibold text-sm"></div>
            </div>
        </div>
        <div date-rangepicker class="flex items-center">
            <div class="relative">
              <div class="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">
                  <svg aria-hidden="true" class="w-5 h-5 text-gray-500 dark:text-gray-400" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M6 2a1 1 0 00-1 1v1H4a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V6a2 2 0 00-2-2h-1V3a1 1 0 10-2 0v1H7V3a1 1 0 00-1-1zm0 5a1 1 0 000 2h8a1 1 0 100-2H6z" clip-rule="evenodd"></path></svg>
              </div>
              <input name="start" type="text" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full pl-10 p-2.5  dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" placeholder="Select date start" value="{{ $start_date }}">
            </div>
            <span class="mx-4 text-gray-500">to</span>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">
                  <svg aria-hidden="true" class="w-5 h-5 text-gray-500 dark:text-gray-400" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M6 2a1 1 0 00-1 1v1H4a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V6a2 2 0 00-2-2h-1V3a1 1 0 10-2 0v1H7V3a1 1 0 00-1-1zm0 5a1 1 0 000 2h8a1 1 0 100-2H6z" clip-rule="evenodd"></path></svg>
              </div>
              <input name="end" type="text" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full pl-10 p-2.5  dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" placeholder="Select date end" value="{{ $end_date }}">
          </div>
          <div class="relative">
            <button type="submit" class="ml-5 text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 mr-2 mb-2 dark:bg-blue-600 dark:hover:bg-blue-700 focus:outline-none dark:focus:ring-blue-800 mt-2    ">Go</button>

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
       </div>

        <div class="grid lg:grid-cols-5 md:grid-cols-4 md:gap-5 gap-x-0 gap-y-5 grid-cols-1">
            <x-segment class=""></x-segment>
            <x-segment class="clear-right lg:col-span-4 md:cols-span-3">
                <canvas id="chart" class="w-full max-h-[50vh]"></canvas>
            </x-segment>
            <x-segment class=""></x-segment>
            <x-segment class="clear-right lg:col-span-4 md:cols-span-3 mt-10">
                <canvas id="realtimeChart" class="w-full max-h-[50vh]"></canvas>
            </x-segment>
        </div>
    </div>

    <script>
        const data = {!! $result ?? '""' !!};
        const database = "{{ $database }}";
        const folder = "{{ $folder }}";
        const solenoidValve_actuate = {!! $solenoidValve_actuate ?? "null" !!};
    </script>
</x-guest-layout>
