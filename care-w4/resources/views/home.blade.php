<x-guest-layout>
@section('title', 'Dashboard')
    <div class="grid md:grid-cols-4 md:gap-10 grid-cols-1 gap-x-0 gap-y-7">
        @foreach ($databases as $name => $folders)
            <a href="/{{ $name }}/{{ array_key_first($folders) ?? '' }}">
                <x-card title="{{ $name }}" subtitle="Database"/> 
            </a>
        @endforeach
    </div>
</x-guest-layout>
