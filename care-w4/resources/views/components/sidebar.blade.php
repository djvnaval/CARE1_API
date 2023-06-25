<aside id="sidebar-multi-level-sidebar" class="fixed top-0 left-0 z-40 w-64 h-screen transition-transform -translate-x-full sm:translate-x-0" aria-label="Sidebar">
    <div class="h-full px-3 py-4 overflow-y-auto bg-gray-50 dark:bg-gray-800">
       <ul class="space-y-2 font-medium">
        <li>
            <header class="md:p-6 p-4 flex items-centerdark:shadow-none dark:outline dark:outline-2 dark:outline-gray-500">
                <a href="/" class="flex items-center gap-2">
                    <img src="{{ Vite::asset('/resources/image/flower.svg') }}" alt="" class="w-10 inline-block">
                    <span class="text-4xl font-bold">Care1</span>
                </a>
                <nav></nav>
            </header>
        </li>
          <li>
             <a href="#" class="flex items-center p-2 text-gray-900 rounded-lg dark:text-white hover:bg-gray-100 dark:hover:bg-gray-700">
                <svg aria-hidden="true" class="w-6 h-6 text-gray-500 transition duration-75 dark:text-gray-400 group-hover:text-gray-900 dark:group-hover:text-white" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path d="M2 10a8 8 0 018-8v8h8a8 8 0 11-16 0z"></path><path d="M12 2.252A8.014 8.014 0 0117.748 8H12V2.252z"></path></svg>
                <span class="ml-3">Dashboard</span>
             </a>
          </li>

          {{ $slot }}

       </ul>
    </div>
 </aside>