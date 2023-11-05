from django.shortcuts import render
from .forms import QuoteForm
from .models import Material
from tempfile import TemporaryDirectory
from .svg_processing import svglength, calculate_cutprice, extract_svg_colors

# Calculate quote from the uploaded SVG
def quote_view(request):
    if request.method == 'POST':
        form = QuoteForm(request.POST, request.FILES)
        if form.is_valid():
            svg_file = form.cleaned_data['svg_file']
            material = form.cleaned_data['material']

            # Calculate quote using your provided functions
            # Save the file temporarily
            with TemporaryDirectory() as temp_dir:
                file_path = f"{temp_dir}/{svg_file.name}"
                with open(file_path, 'wb+') as destination:
                    for chunk in svg_file.chunks():
                        destination.write(chunk)

                svg_length = svglength(file_path)
                cut_price = calculate_cutprice(svg_length, cutspeed=material.cutting_speed)

            return render(request, 'quotes/result.html', {'cut_price': cut_price})

    else:
        form = QuoteForm()

    return render(request, 'quotes/quote.html', {'form': form})


