@if ($attributes->get('data-visible') != 'null')

    <label class="relative inline-flex items-center cursor-pointer mt-2 mr-4  ">

        <input type="checkbox" value="{{ $attributes->get('value') }}"
            {{ $attributes->merge(['class' => 'sr-only peer']) }} {{ $attributes }}>
        <div
            class="w-14 h-7 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 dark:peer-focus:ring-blue-800 rounded-full peer dark:bg-gray-700 peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-0.5 after:left-[4px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-6 after:w-6 after:transition-all dark:border-gray-600 peer-checked:bg-blue-600">
        </div>
        <span data-input-id='{{ $attributes->get('id') }}'
            class="ml-3 text- font-medium text-gray-900 dark:text-gray-300">
            {{ $slot }}
        </span>
    </label>

@endif
