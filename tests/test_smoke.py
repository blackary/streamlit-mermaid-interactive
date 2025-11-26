def test_import():
    from streamlit_mermaid_interactive import mermaid

    assert mermaid is not None


def test_component_manifest():
    """Test that the component manifest is properly configured."""
    from streamlit.components.v2.manifest_scanner import scan_component_manifests

    manifests = scan_component_manifests()
    manifest_dict = {m.name: m for m, _ in manifests}

    assert "streamlit_mermaid_interactive" in manifest_dict, (
        "Component manifest not found"
    )

    manifest = manifest_dict["streamlit_mermaid_interactive"]
    component_names = [c.name for c in manifest.components]
    assert "mermaid" in component_names, (
        f"mermaid component not found in {component_names}"
    )

    # Check that the mermaid component has asset_dir configured
    mermaid_component = next(c for c in manifest.components if c.name == "mermaid")
    assert mermaid_component.asset_dir == "frontend", (
        f"Expected asset_dir='frontend', got {mermaid_component.asset_dir}"
    )


if __name__ == "__main__":
    test_import()
    test_component_manifest()
    print("All tests passed")
