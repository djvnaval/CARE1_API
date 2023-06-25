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
        <link rel="preconnect" href="https://fonts.bunny.net">
        <link href="https://fonts.bunny.net/css?family=figtree:400,500,600,700&display=swap" rel="stylesheet" />

        <!-- Scripts -->
        @vite(['resources/css/app.css', 'resources/js/app.js'])
    </head>
    <body class="bg-[#FDFDFD] dark:bg-slate-800">
        <div class="font-sans text-gray-900 dark:text-white antialiased ">
            <x-sidebar>
                @foreach ($databases as $database => $folders)
                <li>
                    <button type="button" class="flex items-center w-full p-2 text-gray-900 transition duration-75 rounded-lg group hover:bg-gray-100 dark:text-white dark:hover:bg-gray-700" aria-controls="dropdown-{{ $database }}" data-collapse-toggle="dropdown-{{ $database }}">
                          <svg aria-hidden="true" class="flex-shrink-0 w-6 h-6 text-gray-500 transition duration-75 group-hover:text-gray-900 dark:text-gray-400 dark:group-hover:text-white" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M10 2a4 4 0 00-4 4v1H5a1 1 0 00-.994.89l-1 9A1 1 0 004 18h12a1 1 0 00.994-1.11l-1-9A1 1 0 0015 7h-1V6a4 4 0 00-4-4zm2 5V6a2 2 0 10-4 0v1h4zm-6 3a1 1 0 112 0 1 1 0 01-2 0zm7-1a1 1 0 100 2 1 1 0 000-2z" clip-rule="evenodd"></path></svg>
                          <span class="flex-1 ml-3 text-left whitespace-nowrap" sidebar-toggle-item>{{ $database }}</span>
                          <svg sidebar-toggle-item class="w-6 h-6" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd"></path></svg>
                    </button>
                    
                    <ul id="dropdown-{{ $database }}" class="hidden py-2 space-y-2">
                        @foreach ($folders as $folder)
                            <li>
                                <a href="/{{ $database }}/{{ $folder }}" class="flex items-center w-full p-2 text-gray-900 transition duration-75 rounded-lg pl-11 group hover:bg-gray-100 dark:text-white dark:hover:bg-gray-700">{{ $folder }}</a>
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
                        <div>
                            <h1 class="text-3xl font-semibold my-6">@yield('title')</h1>
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

    </body>
</html>
