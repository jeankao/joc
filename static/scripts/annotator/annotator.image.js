Annotator.Plugin.Image = function(element) {
    if ($('img', element).length === 0)
        return;
    var img = $('img', element);
    return {
        traceMouse: false,
        pluginInit: function() {
            if (!Annotator.supported())
                return;
            let annotator = this.annotator;
            var startPoint = null;
            var activeRect = null;
            var highlights = [];
            var isTouchSupported = 'ontouchstart' in window;
            var prevTouch = null;

            function createHighlight(left, top, width, height, annotation) {
                var div = document.createElement('div');
                $(div).addClass('annotator-hl annotator-img-rect')
                    .offset({left: left, top: top})
                    .width(width)
                    .height(height);
                $('.annotator-wrapper', element).append(div);
                if (annotation) {
                    $(div).data('annotation', annotation)
                        .data('annotation-id', annotation.id);
                    div.rect = {
                        left: left,
                        top: top,
                        right: left + width,
                        bottom: top + height
                    };
                    highlights['d' + annotation.id] = {
                        'div': div,
                        'annotation': annotation
                    };
                    $(div).off('mouseover');
                    $(div).on('mouseover', function(event) {
                        return ;
                        // 暫時不用 ... //
                        var pos = $(event.target).position();
                        var x = pos.left + event.offsetX;
                        var y = pos.top + event.offsetY;
                        var annotations = [];
                        for (let i in highlights) {
                            let highlight = highlights[i];
                            let rect = highlight.div.rect;
                            if (x > rect.left && x < rect.right && y > rect.top && y < rect.bottom)
                                annotations.push(highlight.annotation);
                        }
                        if (annotations.length > 1) {
                            window.setTimeout(function() {
                                annotator.showViewer(annotations, {
                                    left: x,
                                    top: y
                                });
                            }, 100);
                        }
                    });
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

            function markStart(point) {
                annotator.editor.hide();
                self.traceMouse = true;
                startPoint = {
                    x: point.x,
                    y: point.y
                };
                activeRect = createHighlight(point.x, point.y, 0, 0, null);
            }

            function markEnd(point) {
                self.traceMouse = false;
                startPoint = null;
                annotator.viewer.hide();
                annotator.showEditor({
                    text: ''
                }, {
                    left: point.x,
                    top: point.y
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
                    markStart({
                        x: e.offsetX,
                        y: e.offsetY
                    });
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
                        });
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
                    let imgWidth = img.width(), imgHeight = img.height();
                    var rect = item.shapes[0].geometry;
                    createHighlight(rect.x * imgWidth, rect.y * imgHeight, rect.width * imgWidth, rect.height * imgHeight, item);
                }
            });

            this.annotator.subscribe('annotationEditorSubmit', function(editor, annotation) {
                var aid = annotation.id || 0;
                if (!aid) {
                    var rect = {
                        left: activeRect.offsetLeft, 
                        top: activeRect.offsetTop, 
                        width: activeRect.offsetWidth, 
                        height: activeRect.offsetHeight, 
                    };
                    let imgHeight = img.height(), 
                        imgWidth = img.width();
                    annotation.shapes = [{
                        geometry: {
                            y: rect.top / imgHeight,
                            x: rect.left / imgWidth,
                            width: rect.width / imgWidth,
                            height: rect.height / imgHeight,
                        },
                        style: {},
                    }];
                    annotator.publish('annotationCreated', annotation);
                } else
                    annotator.publish('annotationUpdated', annotation);
            });

            this.annotator.subscribe('annotationCreated', function(annotation) {
                var rect = annotation.shapes[0].geometry;
                (function verify_id() {
                    if (!annotation.id) {
                        window.setTimeout(verify_id, 5);
                    } else {
                        let imgWidth = img.width(), imgHeight = img.height();
                        createHighlight(rect.x * imgWidth, rect.y * imgHeight, rect.width * imgWidth, rect.height * imgHeight, annotation);
                    }
                })();
            });
/*
            this.annotator.subscribe("annotationUpdated", function(annotation) {
            });
*/
            this.annotator.subscribe("annotationEditorHidden", function(editor) {
                if (activeRect) {
                    $(activeRect).remove();
                    activeRect = null;
                }
            });

            this.annotator.subscribe("annotationDeleted", function(annotation) {
                let highlight = highlights['d' + annotation.id];
                if (highlight) {
                    $(highlight.div).remove();
                    delete highlights['d' + annotation.id];
                }
            });
        },
    }
};

//---------------------------------------------------------------------------

function userAnnotationInit(userid, lesson, page) {
    $('img.annotate').each(function(index, element) {
        $(element).wrap("<div></div>").parent().annotator()
            .annotator('addPlugin', 'Store', {
                prefix: '/annotate', 
                annotationData: {
                    'lesson': lesson, 
                    'page': page, 
                    'img': (new URL(element.src)).pathname,
                    'userid': userid,
                }, 
                loadFromSearch: {
                    'userid': userid, 
                    'img': (new URL(element.src)).pathname,
                }
            })
            .annotator('addPlugin', 'Touch')
            .annotator('addPlugin', 'Image');
    });
}