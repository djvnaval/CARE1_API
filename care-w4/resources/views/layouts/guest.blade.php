@php
    use App\Http\Controllers\Chart;

    $databases = Chart::databases();
@endphp

<!DOCTYPE html>
<html lang="{{ str_replace('_', '-', app()->getLocale()) }}">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <meta name="csrf-token" content="{{ csrf_token() }}">

        <title>@yield('title') - {{ config('app.name', 'Laravel') }}</title>

        <!-- Fonts -->
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700&display=swap" rel="stylesheet">
        <link rel="stylesheet" type="text/css" href="https://cdn.jsdelivr.net/npm/daterangepicker/daterangepicker.css" />
        <!-- Scripts -->
        @vite(['resources/css/app.css', 'resources/js/app.js'])
    </head>
    <body class="relative bg-[#242529]">
        <x-toast-danger></x-toast-danger>
        <x-toast-warning></x-toast-warning>

        <div class="font-sans  text-white antialiased ">
            <x-sidebar>
                @foreach ($databases as $database => $folders)
                <li>
                    <button type="button" class="flex items-center w-full p-2 text-white truncate transition duration-75 rounded-lg group hover:bg-cream hover:text-black dark:hover:bg-gray-700" aria-controls="dropdown-{{ $database }}" data-collapse-toggle="dropdown-{{ $database }}">  
                        <span class="flex-1 ml-3 text-left whitespace-nowrap" sidebar-toggle-item>{{ $database }}</span>
                        <svg sidebar-toggle-item class="w-6 h-6" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd"></path></svg>
                    </button>
                    
                    <ul id="dropdown-{{ $database }}" class="hidden py-2 space-y-2">
                        @foreach ($folders as $folder => $description)
                            <li>
                                <a href="/{{ $database }}/{{ $folder }}" class="flex items-center w-full p-2 text-white transition duration-75 rounded-lg pl-11 group hover:bg-cream hover:text-black dark:text-white dark:hover:bg-gray-700">{{ $folder }}</a>
                            </li>
                        @endforeach
                    </ul>
                 </li>
                @endforeach
            </x-sidebar>
            <main class="sm:ml-64">
                <div class="md:p-6 p-4 mx-auto">
                    <x-breadcrumb>@yield('breadcrumb')</x-breadcrumb>
                    <div class="grid grid-cols-2 ">
                        <div class="my-6">
                            <h1 class="text-3xl font-medium ">@yield('title')</h1>
                            <p class="text-md mt-2">@yield('description')</p>
                        </div>

                        <div class="text-right ">
                            @yield('controls')
                        </div>
                    </div>

                    {{ $slot }}
                </div>
            </main>
        </div>
        
        <script src="https://cdnjs.cloudflare.com/ajax/libs/flowbite/1.6.5/datepicker.min.js"></script>
        
        <script type="text/javascript" src="https://cdn.jsdelivr.net/jquery/latest/jquery.min.js"></script>
        <script type="text/javascript" src="https://cdn.jsdelivr.net/momentjs/latest/moment.min.js"></script>
        <script type="text/javascript" src="https://cdn.jsdelivr.net/npm/daterangepicker/daterangepicker.min.js"></script>
    </body>
</html>
