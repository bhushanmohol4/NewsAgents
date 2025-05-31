import json
import os
import re
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Dict, Any, Type
from Logging.Logger import logger

def _clean_json_content(content: str) -> str:
        """
        Clean the JSON content by removing think tags and any non-JSON text.
        
        Args:
            content (str): The raw content from the file
            
        Returns:
            str: Cleaned JSON content
        """
        logger.info("Cleaning JSON content")
        # Remove think tags and their content
        content = re.sub(r'<think>.*?</think>', '', content, flags=re.DOTALL)
        
        # Find the first [ and last ] to extract just the JSON array
        start = content.find('[')
        end = content.rfind(']') + 1
        
        if start == -1 or end == 0:
            logger.error("No valid JSON array found in the content")
            raise ValueError("No valid JSON array found in the content")
            
        logger.info("Extracting JSON content")
        return content[start:end]

class ReadScriptInput(BaseModel):
        input_file: str = Field(..., description="Path to the input JSON file")
        output_file: str = Field(..., description="Path to save the cleaned JSON file")

class ReadScriptTool(BaseTool):
    name: str = "Read Script File Tool"
    description: str = "Reads and parses the podcast script JSON file."
    args_schema: Type[BaseModel] = ReadScriptInput

    def _run(self, input_file: str, output_file: str) -> Dict[str, Any]:
        """
        Read and parse the podcast script JSON file.
        
        Args:
            script_file (str): Path to the JSON script file
            
        Returns:
            Dict[str, Any]: The parsed script data
            
        Raises:
            FileNotFoundError: If the script file doesn't exist
            json.JSONDecodeError: If the file contains invalid JSON
            ValueError: If the script format is invalid
        """
        logger.info("Reading script file")
        if not os.path.exists(input_file):
            logger.error("Script file not found: %s", input_file)
            raise FileNotFoundError(f"Script file not found: {input_file}")
            
        try:
            # Open the file
            with open(input_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Clean the content
            cleaned_content = _clean_json_content(content)
            logger.info("Cleaned content: %s", cleaned_content)
            
            # Parse the cleaned JSON
            data = json.loads(cleaned_content)
                
            # Validate script format
            if not isinstance(data, list):
                logger.error("Script must be a list of dialogue entries")
                raise ValueError("Script must be a list of dialogue entries")
                
            for entry in data:
                if not isinstance(entry, dict):
                    logger.error("Each dialogue entry must be a dictionary")
                    raise ValueError("Each dialogue entry must be a dictionary")
                if 'speaker' not in entry or 'text' not in entry:
                    logger.error("Each dialogue entry must have 'speaker' and 'text' fields")
                    raise ValueError("Each dialogue entry must have 'speaker' and 'text' fields")
            
            logger.info("Script parsed successfully")

            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
            
            logger.info(f"Cleaned script saved to: {output_file}")

            return data
            
        except json.JSONDecodeError as e:
            logger.error("Invalid JSON format in script file: %s", str(e))
            raise ValueError(f"Invalid JSON format in script file: {str(e)}")
        except Exception as e:
            logger.error("Error reading script file: %s", str(e))
            raise Exception(f"Error reading script file: {str(e)}")