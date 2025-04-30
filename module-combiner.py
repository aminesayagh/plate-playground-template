import os
from datetime import datetime


class ModuleCombinerConfig:
    """
    Configuration class for the module combiner.
    Update these settings as needed before running the script.
    """
    def __init__(self):
        # Source directories and/or files to include
        # Can contain directory paths and/or file paths
        self.sources = ["./src"]
        
        # Output file path
        self.output_file = "modules_summary.md"
        
        # File extensions to include (default: Python files only)
        self.file_extensions = ['.py']
        
        # Title for the generated markdown document
        self.document_title = "Python Modules Summary"
        
        # Include table of contents
        self.include_toc = True
        
        # Include metadata (generation date, file count, etc.)
        self.include_metadata = True
        
        # Files or directories to exclude (exact names or patterns)
        self.exclude_patterns = ['__pycache__', 'venv', '.git', '.idea']
        
        # Group files by repository/source directory in the output
        self.group_by_source = True
        
        # Repository names (if None, will use directory names)
        # Should match the order of source_directories if provided
        self.repository_names = None


def get_files_by_extension(directory, config):
    """
    Get all files with specified extensions from a directory and its subdirectories.
    Returns a list of file paths.
    """
    matching_files = []
    
    for root, dirs, files in os.walk(directory):
        # Skip directories that match exclude patterns
        dirs[:] = [d for d in dirs if not any(pattern in d for pattern in config.exclude_patterns)]
        
        for file in files:
            # Skip files that match exclude patterns
            if any(pattern in file for pattern in config.exclude_patterns):
                continue
                
            if any(file.endswith(ext) for ext in config.file_extensions):
                matching_files.append(os.path.join(root, file))
    
    return sorted(matching_files)


def extract_file_content(file_path):
    """
    Extract the content of a file.
    Returns the content as a string.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        return f"ERROR: Could not read file {file_path}. Error: {str(e)}"


def generate_markdown(files, base_dir, config):
    """
    Generate markdown content from files.
    Returns the markdown content as a string.
    """
    markdown = f"# {config.document_title}\n\n"
    
    if config.include_metadata:
        markdown += f"Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        markdown += f"Source directory: `{base_dir}`\n\n"
        markdown += f"Total files: {len(files)}\n\n"
    
    # Table of contents
    if config.include_toc:
        markdown += "## Table of Contents\n\n"
        for file_path in files:
            relative_path = os.path.relpath(file_path, base_dir)
            file_anchor = relative_path.replace('/', '-').replace('\\', '-').replace('.', '-')
            markdown += f"- [{relative_path}](#{file_anchor})\n"
        
        markdown += "\n"
    
    # File contents
    for file_path in files:
        relative_path = os.path.relpath(file_path, base_dir)
        file_anchor = relative_path.replace('/', '-').replace('\\', '-').replace('.', '-')
        file_extension = os.path.splitext(file_path)[1][1:]  # Get extension without the dot
        
        markdown += f"## {relative_path} {{{file_anchor}}}\n\n"
        markdown += f"```{file_extension}\n"
        markdown += extract_file_content(file_path)
        markdown += "\n```\n\n"
    
    return markdown


def generate_grouped_markdown(repo_file_map, config):
    """
    Generate markdown content with files grouped by repository.
    Returns the markdown content as a string.
    """
    markdown = f"# {config.document_title}\n\n"
    
    if config.include_metadata:
        markdown += f"Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        # Count total files across all repositories
        total_files = sum(len(repo_info['files']) for repo_info in repo_file_map.values())
        markdown += f"Total repositories/sources: {len(repo_file_map)}\n"
        markdown += f"Total files: {total_files}\n\n"
    
    # Master table of contents if needed
    if config.include_toc:
        markdown += "## Sources\n\n"
        
        for repo_name in repo_file_map:
            repo_anchor = repo_name.replace(' ', '-').replace('/', '-').replace('\\', '-').replace('.', '-')
            markdown += f"- [{repo_name}](#{repo_anchor})\n"
        
        markdown += "\n"
    
    # Process each repository
    for repo_name, repo_info in repo_file_map.items():
        repo_anchor = repo_name.replace(' ', '-').replace('/', '-').replace('\\', '-').replace('.', '-')
        directory = repo_info['directory']
        files = repo_info['files']
        
        markdown += f"# {repo_name} {{{repo_anchor}}}\n\n"
        markdown += f"Source: `{directory}`\n"
        markdown += f"Files: {len(files)}\n\n"
        
        # Repository-specific table of contents
        if config.include_toc and len(files) > 1:  # Only show TOC if there's more than one file
            markdown += f"## {repo_name} - Table of Contents\n\n"
            
            for file_path in files:
                # For individual files, just use the filename
                if os.path.isfile(directory):
                    file_name = os.path.basename(file_path)
                    file_anchor = f"{repo_anchor}-{file_name.replace('.', '-')}"
                    markdown += f"- [{file_name}](#{file_anchor})\n"
                else:
                    # For directories, use relative path
                    relative_path = os.path.relpath(file_path, directory)
                    file_anchor = f"{repo_anchor}-{relative_path.replace('/', '-').replace('\\', '-').replace('.', '-')}"
                    markdown += f"- [{relative_path}](#{file_anchor})\n"
            
            markdown += "\n"
        
        # File contents for this repository
        for file_path in files:
            if os.path.isfile(directory):
                # For individual files
                file_name = os.path.basename(file_path)
                file_anchor = f"{repo_anchor}-{file_name.replace('.', '-')}"
                file_extension = os.path.splitext(file_path)[1][1:]
                
                markdown += f"## {file_name} {{{file_anchor}}}\n\n"
            else:
                # For directories
                relative_path = os.path.relpath(file_path, directory)
                file_anchor = f"{repo_anchor}-{relative_path.replace('/', '-').replace('\\', '-').replace('.', '-')}"
                file_extension = os.path.splitext(file_path)[1][1:]
                
                markdown += f"## {relative_path} {{{file_anchor}}}\n\n"
            
            markdown += f"```{file_extension}\n"
            markdown += extract_file_content(file_path)
            markdown += "\n```\n\n"
    
    return markdown


def save_markdown(markdown, output_file):
    """
    Save markdown content to a file.
    """
    try:
        # Ensure the directory exists
        output_dir = os.path.dirname(output_file)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(markdown)
        return True
    except Exception as e:
        print(f"ERROR: Could not write to file {output_file}. Error: {str(e)}")
        return False


def process_source(source, config):
    """
    Process a source (file or directory) and return its files.
    """
    if os.path.isfile(source):
        # Check if file extension matches allowed extensions
        if any(source.endswith(ext) for ext in config.file_extensions):
            return [source]
        else:
            print(f"Skipping {source} - extension not in allowed list: {config.file_extensions}")
            return []
    elif os.path.isdir(source):
        # Process directory
        return get_files_by_extension(source, config)
    else:
        print(f"WARNING: Source not found: {source}")
        return []


def run_combiner(config=None):
    """
    Run the module combiner with the given configuration.
    """
    if config is None:
        config = ModuleCombinerConfig()
    
    # For backward compatibility
    if hasattr(config, 'source_directories') and not hasattr(config, 'sources'):
        if isinstance(config.source_directories, str):
            config.sources = [config.source_directories]
        else:
            config.sources = config.source_directories
    
    # Convert single source to list for uniform processing
    if isinstance(config.sources, str):
        config.sources = [config.sources]
    
    # Initialize repository names if not provided
    if config.repository_names is None:
        config.repository_names = []
        for source in config.sources:
            if os.path.isfile(source):
                # For files, use filename
                config.repository_names.append(os.path.basename(source))
            elif os.path.isdir(source):
                # For directories, use directory name
                dir_name = os.path.basename(os.path.abspath(source))
                config.repository_names.append(dir_name or source)
            else:
                config.repository_names.append(f"Unknown source: {source}")
    
    # Ensure we have the same number of names as sources
    if len(config.repository_names) != len(config.sources):
        print("WARNING: Number of repository names doesn't match number of sources.")
        config.repository_names = config.repository_names[:len(config.sources)]
        while len(config.repository_names) < len(config.sources):
            source = config.sources[len(config.repository_names)]
            if os.path.isfile(source):
                config.repository_names.append(os.path.basename(source))
            elif os.path.isdir(source):
                dir_name = os.path.basename(os.path.abspath(source))
                config.repository_names.append(dir_name or f"Repository {len(config.repository_names) + 1}")
            else:
                config.repository_names.append(f"Unknown source {len(config.repository_names) + 1}")
    
    # Get all files from all sources
    all_files = []
    repo_file_map = {}  # Maps repository to its files
    
    for i, source in enumerate(config.sources):
        repo_name = config.repository_names[i]
        
        # Process source (file or directory)
        matching_files = process_source(source, config)
        
        if matching_files:
            all_files.extend(matching_files)
            repo_file_map[repo_name] = {
                'directory': source,  # This can be a file or directory path
                'files': matching_files
            }
            print(f"Found {len(matching_files)} files in {repo_name}")
        else:
            print(f"No matching files found in {repo_name}")
    
    if not all_files:
        print(f"No matching files found in any of the specified sources.")
        return 0
    
    # Generate markdown based on grouping setting
    if config.group_by_source:
        markdown = generate_grouped_markdown(repo_file_map, config)
    else:
        # Try to find common path or use current directory as base
        if len(config.sources) > 1:
            try:
                common_path = os.path.commonpath([os.path.abspath(s) for s in config.sources])
            except ValueError:
                # No common path (e.g., different drives on Windows)
                common_path = os.getcwd()
        else:
            # For a single source, use its parent directory
            source_path = os.path.abspath(config.sources[0])
            if os.path.isfile(source_path):
                common_path = os.path.dirname(source_path)
            else:
                common_path = source_path
        
        markdown = generate_markdown(all_files, common_path, config)
    
    # Save markdown
    success = save_markdown(markdown, config.output_file)
    
    if success:
        print(f"Successfully generated {config.output_file} with {len(all_files)} files from {len(repo_file_map)} sources.")
    
    return 0


if __name__ == "__main__":
    # Create a configuration object with custom settings
    config = ModuleCombinerConfig()
    source_directories = "C:/Users/ROG ZEPHYRUS/Desktop/dev/plate-playground-template"
    # Example: Update configuration with both directories and individual files
    config.sources = [
        source_directories + "/src",
        source_directories + "/package.json"
    ]
    
    # Optional: Custom names
    config.repository_names = [
        "Source Code",
        "Config"
    ]
    
    config.output_file = "combined_modules.md"
    config.file_extensions = ['.tsx', '.ts', '.json']
    
    # Run the combiner with the custom configuration
    exit(run_combiner(config))