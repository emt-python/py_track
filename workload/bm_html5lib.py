"""Wrapper script for testing the performance of the html5lib HTML 5 parser.

The input data is the spec document for HTML 5, written in HTML 5.
The spec was pulled from http://svn.whatwg.org/webapps/index.
"""
from html5lib.serializer import serialize
import html5lib
import time
import io
import os
cur_dir = os.path.dirname(os.path.realpath(__file__))


def bench_html5lib(html_file):
    html_file.seek(0)
    html5lib.parse(html_file)


def replicate_and_parse_html_content(html_content, replication_factor=10):
    """
    Parses the HTML content with html5lib, then replicates the body's inner HTML
    to increase memory usage, and serializes it back to HTML.
    """
    # Parse the initial HTML content
    parser = html5lib.HTMLParser(
        tree=html5lib.treebuilders.getTreeBuilder("dom"))
    document = parser.parse(html_content)

    # Find the body element and serialize it to a string
    body = document.getElementsByTagName('body')[0]
    serialized_body_content = serialize(body, tree="dom")

    # Replicate the serialized body content
    body_content_replicated = ''.join(
        serialized_body_content for _ in range(replication_factor))

    # For demonstration, this would be the point to re-parse or use the replicated content
    # In this example, we're directly manipulating the string, so re-parsing isn't shown
    # But this string represents the replicated body content, significantly increasing the potential memory usage

    return body_content_replicated


def increase_memory_traffic_with_html_content(replicated_content, iterations=5):
    """
    Parses and modifies the replicated HTML content multiple times to increase memory traffic.
    """
    parser = html5lib.HTMLParser(
        tree=html5lib.treebuilders.getTreeBuilder("dom"))
    final_document = None

    for _ in range(iterations):
        # Parse the replicated content to create a new DOM tree
        document = parser.parse("<body>" + replicated_content + "</body>")

        # Modify the document by adding new elements, increasing its size
        body = document.getElementsByTagName('body')[0]
        for i in range(100):
            new_element = document.createElement('div')
            new_element.textContent = "Additional content to increase memory usage."
            body.appendChild(new_element)

        # Serialize the modified document back to HTML
        modified_content = serialize(document, tree="dom")
        # Append the modified content for the next iteration
        replicated_content += modified_content

        final_document = document  # Keep the last version for potential use

    return final_document


if __name__ == "__main__":
    filename = os.path.join(cur_dir, "w3_tr_html5.html")
    with open(filename, "rb") as fp:
        html_file = io.BytesIO(fp.read())
    start_time = time.time()
    for i in range(1):
        # bench_html5lib(html_file)
        replicated_body_content = replicate_and_parse_html_content(
            html_file, 10)
        final_document = increase_memory_traffic_with_html_content(
            replicated_body_content, iterations=5)
    elapsed_time = time.time() - start_time
    print(f"Compute time: {elapsed_time:.2f} seconds")
