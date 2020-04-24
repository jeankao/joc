Annotator.Plugin.Image = function(element) {
    if ($('img', element).length === 0)
        return;
    return {
        traceMouse: false,
        pluginInit: function() {
            if (!Annotator.supported())
                return;
            let annotator = this.annotator;
            var startPoint = null;
            var currentImg = null;
            var activeRect = null;
            var isTouchSupported = 'ontouchstart' in window;
            var prevTouch = null;

            // Create Image Wrapper Div
            $('img', element).each(function(index, img) {
                var img_wrapper = document.createElement('div');
                $(img_wrapper).addClass('annotator-img-wrapper');
                $(img).before(img_wrapper);
                $(img_wrapper).append(img);
            });

            function createHighlight(left, top, width, height, img, annotation) {
                var div = document.createElement('div');
                $(div).addClass('annotator-hl annotator-img-rect')
                    .offset({left: left, top: top})
                    .width(width)
                    .height(height);
                $(img).parent().append(div);
                if (annotation) {
                    $(div).data('annotation', annotation)
                        .data('annotation-id', annotation.id);
                    $(div).off('mouseover');
                } else {
                    $(div).off('mouseover');
                    $(div).on('mouseover', function(event) {
                        event.preventDefault();
                        return false;
                    });
                    $(div).off('mousemove');
                    $(div).on('mousemove', function(event) {
                        event.preventDefault();
                        return false;
                    });
                }
                return div;
            }

            function markStart(point, img) {
                annotator.editor.hide();
                self.traceMouse = true;
                startPoint = {
                    x: point.x,
                    y: point.y
                };
                activeRect = createHighlight(point.x, point.y, 0, 0, img, null);
            }

            function markEnd(point) {
                self.traceMouse = false;
                startPoint = null;
                annotator.viewer.hide();
                var offset = $(currentImg).offset();
                var woffset = $('.annotator-wrapper', element).offset();
                annotator.showEditor({
                    text: ''
                }, {
                    left: point.x + offset.left - woffset.left,
                    top: point.y + offset.top - woffset.top,
                });
            }

            function markMove(point) {
                $(activeRect).css({
                    left: Math.min(point.x, startPoint.x),
                    top: Math.min(point.y, startPoint.y),
                    width: Math.abs(point.x - startPoint.x) + 'px',
                    height: Math.abs(point.y - startPoint.y) + 'px'
                });
            }

            $('img', element).on('mousedown', function(e) {
                if (!annotator.options.readOnly && e.which === 1) {
                    currentImg = e.target;
                    markStart({
                        x: e.offsetX,
                        y: e.offsetY
                    }, e.target);
                }
                return false;
            });

            $('img', element).on('mouseup', function(e) {
                if (!annotator.options.readOnly) {
                    markEnd({
                        x: e.offsetX,
                        y: e.offsetY
                    });
                }
                return false;
            });

            $('img', element).on('mousemove', function(e) {
                if (self.traceMouse) {
                    markMove({
                        x: e.offsetX,
                        y: e.offsetY
                    });
                    if (e.originalEvent.buttons === 0) {
                        e.type = 'mouseup';
                        $('img', element).trigger(e);
                    }
                }
                return false;
            });

            if (isTouchSupported) {
                $('img', element).on('touchstart', function(e) {
                    if (!annotator.options.readOnly) {
                        e.preventDefault();
                        markStart({
                            x: e.touches[0].pageX - e.target.x,
                            y: e.touches[0].pageY - e.target.y
                        }, e.target);
                    }
                });
                $('img', element).on('touchend', function(e) {
                    if (!annotator.options.readOnly) {
                        e.preventDefault();
                        markEnd(prevTouch);
                    }
                });
                $('img', element).on('touchmove', function(e) {
                    if (self.traceMouse) {
                        e.preventDefault();
                        prevTouch = {
                            x: e.touches[0].pageX - e.target.x,
                            y: e.touches[0].pageY - e.target.y
                        };
                        markMove(prevTouch);
                    }
                });
            }

            this.annotator.subscribe("annotationsLoaded", function(annotations) {
                for (let i in annotations) {
                    let item = annotations[i];
                    if (!item.shapes)   // ignore non-image annotations
                        continue;
                    var img = $("img[src='"+item.img+"']", element)[0];
                    var rect = item.shapes[0].geometry;
                    var imgWidth = $(img).width();
                    var imgHeight = $(img).height();
                        
                    createHighlight(rect.x * imgWidth, rect.y * imgHeight, rect.width * imgWidth, rect.height * imgHeight, img, item);
                }
            });

            this.annotator.subscribe('annotationEditorSubmit', function(editor, annotation) {
                var aid = annotation.id || 0;
                if (!activeRect)
                    return;
                if (!aid) {
                    var imgHeight = $(currentImg).height(), 
                        imgWidth = $(currentImg).width();
                    
                    annotation.img = (new URL(currentImg.src)).pathname;
                    annotation.shapes = [{
                        geometry: {
                            y: activeRect.offsetTop / imgHeight,
                            x: activeRect.offsetLeft / imgWidth,
                            width: activeRect.offsetWidth / imgWidth,
                            height: activeRect.offsetHeight / imgHeight,
                        },
                    }];
                    annotator.publish('annotationCreated', annotation);
                } else {
                    annotator.publish('annotationUpdated', annotation);
                }
            });

            this.annotator.subscribe('annotationCreated', function(annotation) {
                if (!annotation.shapes)
                    return;
                var rect = annotation.shapes[0].geometry;
                (function verify_id() {
                    if (!annotation.id) {
                        window.setTimeout(verify_id, 5);
                    } else {
                        var imgHeight = $(currentImg).height(), 
                            imgWidth = $(currentImg).width();
                        createHighlight(rect.x * imgWidth, rect.y * imgHeight, rect.width * imgWidth, rect.height * imgHeight, currentImg, annotation);
                    }
                })();
            });

            // this.annotator.subscribe("annotationUpdated", function(annotation) {
            //     modifyHighlightColor(annotation);
            // });

            this.annotator.subscribe("annotationEditorHidden", function(editor) {
                if (activeRect) {
                    $(activeRect).remove();
                    activeRect = null;
                }
            });

            this.annotator.subscribe("annotationDeleted", function(annotation) {
                if (annotation.img) {
                    $(".annotator-img-rect").each(function(index, div) {
                        if (annotation.id == $(div).data('annotation-id'))
                            $(div).remove();
                    });
                }
            });
        },
    }
}

//---------------------------------------------------------------------------
function userAnnotationInit(userid, lesson, unit) {
    $('div.annotate').each(function(index, element) {
        $(element).annotator()
            .annotator('addPlugin', 'Store', {
                prefix: '/annotate', 
                annotationData: {
                    'userid': userid,
                    'lesson': lesson, 
                    'unit': unit,
                },
                loadFromSearch: {
                    'userid': userid,
                    'lesson': lesson, 
                    'unit': unit,
                },
            })
            .annotator('addPlugin', 'Touch')
            .annotator('addPlugin', 'Image');
    });
}