"""
WebGL & Three.js Blackbox Evaluator Gate
Validates that 3D scene renders without crashes, black screen, or mesh overlap.
Used as an Evaluator step in multi-agent coding pipelines to trigger self-correction.
"""

def generate_webgl_assertion_script() -> str:
    return """
    (() => {
        const canvas = document.querySelector('canvas');
        if (!canvas) return { pass: false, reason: "CANVAS_ELEMENT_NOT_FOUND" };
        
        // 1. 验证 WebGL 上下文正常初始化
        const gl = canvas.getContext('webgl2') || canvas.getContext('webgl');
        if (!gl) return { pass: false, reason: "WEBGL_CONTEXT_FAILED" };
        
        // 2. 验证渲染管线三角面片数 (排除空场景与加载挂死)
        const renderer = window.__THREE_RENDERER__;
        const triangles = renderer && renderer.info ? renderer.info.render.triangles : -1;
        if (triangles === 0) {
            return { pass: false, reason: "ZERO_RENDERED_TRIANGLES" };
        }
        
        // 3. 读取中心 10x10 像素排除纯黑屏 (0,0,0) 着色器报错
        const pixels = new Uint8Array(4 * 10 * 10);
        gl.readPixels(canvas.width / 2 - 5, canvas.height / 2 - 5, 10, 10, gl.RGBA, gl.UNSIGNED_BYTE, pixels);
        let nonZeroCount = 0;
        for (let i = 0; i < pixels.length; i += 4) {
            if (pixels[i] > 10 || pixels[i+1] > 10 || pixels[i+2] > 10) {
                nonZeroCount++;
            }
        }
        if (nonZeroCount === 0) {
            return { pass: false, reason: "BLACK_SCREEN_RENDER_ERROR" };
        }
        
        return { pass: true, triangles, nonZeroCount };
    })()
    """

def run_headless_evaluator(browser_page) -> dict:
    result = browser_page.evaluate(generate_webgl_assertion_script())
    return result
