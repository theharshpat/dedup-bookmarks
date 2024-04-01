def extract_info_from_line(line):
    # Extract the URL
    start_url = line.find('HREF="') + 6
    end_url = line.find('"', start_url)
    url = line[start_url:end_url]

    # Extract the title
    start_title = line.find('>', end_url) + 1
    end_title = line.find('</A', start_title)
    title = line[start_title:end_title]

    return url, title

def deduplicate_urls(input_filepath, output_filepath):
    unique_entries = {}
    total_lines = 0
    duplicates = 0
    
    with open(input_filepath, 'r', encoding='utf-8') as file:
        for line in file:
            total_lines += 1
            url, title = extract_info_from_line(line)
            
            # If the URL has not been encountered before, save the line
            if url not in unique_entries:
                unique_entries[url] = (title, line)
            else:
                # Check if the titles are different
                existing_title, _ = unique_entries[url]
                if title != existing_title:
                    print(f"Duplicate URL with different titles found:\n1. {existing_title}\n2. {title}\nPlease select which one to keep (1/2): ")
                    choice = input()
                    if choice == '2':
                        # Update to keep the new title and line
                        unique_entries[url] = (title, line)
                duplicates += 1

    # Write the chosen lines to the output file
    with open(output_filepath, 'w', encoding='utf-8') as file:
        for _, line in unique_entries.values():
            file.write(line)
    
    # Print metrics
    print(f'Total lines processed: {total_lines}')
    print(f'Unique URLs found: {len(unique_entries)}')
    print(f'Duplicates found: {duplicates}')

# Replace 'input.html' with the path to your input file
input_filepath = 'input.html'
# The output file will be saved as 'output.html'
output_filepath = 'output.html'

deduplicate_urls(input_filepath, output_filepath)
