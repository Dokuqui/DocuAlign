export interface TextBlock {
    x0: number;
    y0: number;
    x1: number;
    y1: number;
    text: string;
    page_num: number;
}

export interface DocumentTextBlocks {
    document_id: string;
    blocks: TextBlock[];
}

export interface TextEdit {
    page_num: number;
    redact_coords: number[];
    new_text: string;
    insert_coords: number[];
}

export interface DocumentEditRequest {
    edits: TextEdit[];
    fontname: string;
    fontsize: number;
}