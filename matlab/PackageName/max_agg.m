function result = max_agg(data, column)
    % max_agg - Maximum value in a column.
    %
    % Args:
    %   data: Numeric array or struct array.
    %   column: Field name (for struct data) or empty (for numeric data).
    %
    % Returns:
    %   Maximum value, or [] if empty or all NaN.

    if isempty(data)
        result = [];
        return;
    end

    values = extract_values(data, column);
    values = values(~isnan(values));

    if isempty(values)
        result = [];
    else
        result = max(values);
    end
end

function values = extract_values(data, column)
    if isstruct(data)
        values = [data.(column)];
    else
        values = data(:)';
    end
end
